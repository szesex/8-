// skills/interclaw_coordinator.js
// Server-side coordinator for InterClaw multi-agent system
// Manages agent registry, heartbeats, and task routing
//
// Storage: in-memory + JSON persistence at /home/node/.openclaw/workspace/state/interclaw_state.json

import fs from "fs";
import path from "path";

const STATE_FILE = "/home/node/.openclaw/workspace/state/interclaw_state.json";
const HEARTBEAT_TIMEOUT_MS = 90 * 1000; // 90s without heartbeat = offline

// ---------- State load/save ----------
let _state = { agents: {}, tasks: [] };

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      const raw = fs.readFileSync(STATE_FILE, "utf-8");
      _state = JSON.parse(raw);
      if (!_state.agents) _state.agents = {};
      if (!_state.tasks) _state.tasks = [];
    }
  } catch (e) {
    console.error("[InterClaw coordinator] Failed to load state:", e.message);
  }
}

function saveState() {
  try {
    fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(_state, null, 2));
  } catch (e) {
    console.error("[InterClaw coordinator] Failed to save state:", e.message);
  }
}

loadState();

// ---------- API methods ----------
const skill = {
  registerAgent({ agent_id, skills = [], metadata = {} }) {
    if (!agent_id) throw new Error("agent_id required");
    const isNew = !_state.agents[agent_id];
    _state.agents[agent_id] = {
      agent_id,
      skills,
      metadata,
      registered_at: _state.agents[agent_id]?.registered_at || new Date().toISOString(),
      last_heartbeat: new Date().toISOString(),
      online: true,
    };
    saveState();
    console.log(`[InterClaw coordinator] ${isNew ? "Registered" : "Re-registered"} ${agent_id} (skills: ${skills.join(", ")})`);
    return { ok: true, agent_id, status: isNew ? "new" : "renewed" };
  },

  heartbeat({ agent_id }) {
    if (!agent_id) throw new Error("agent_id required");
    if (!_state.agents[agent_id]) {
      // Auto-register if not seen
      _state.agents[agent_id] = {
        agent_id,
        skills: [],
        metadata: {},
        registered_at: new Date().toISOString(),
      };
    }
    _state.agents[agent_id].last_heartbeat = new Date().toISOString();
    _state.agents[agent_id].online = true;
    saveState();
    return { ok: true, agent_id, ts: _state.agents[agent_id].last_heartbeat };
  },

  sendTask({ from_agent, to, task_type, payload = {} }) {
    if (!from_agent) throw new Error("from_agent required");
    if (!task_type) throw new Error("task_type required");

    // Auto-route if no `to` specified: pick first online agent with matching skills
    let targetAgent = to;
    if (!targetAgent) {
      const candidates = Object.values(_state.agents)
        .filter(a => a.online && (Date.now() - new Date(a.last_heartbeat).getTime() < HEARTBEAT_TIMEOUT_MS));
      // Prefer agents whose skills include task_type, else fall back to first online
      const matched = candidates.find(a => a.skills.includes(task_type));
      targetAgent = matched?.agent_id || candidates[0]?.agent_id || null;
    }

    if (!targetAgent) {
      throw new Error(`No online agents to route task "${task_type}"`);
    }

    const task = {
      id: `task_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      from_agent,
      to_agent: targetAgent,
      task_type,
      payload,
      status: "pending",
      created_at: new Date().toISOString(),
    };
    _state.tasks.push(task);
    saveState();
    console.log(`[InterClaw coordinator] Routed ${task.id} (${task_type}) from ${from_agent} → ${targetAgent}`);
    return { ok: true, task };
  },

  getMyTasks({ agent_id }) {
    if (!agent_id) throw new Error("agent_id required");
    const tasks = _state.tasks.filter(t => t.to_agent === agent_id && t.status === "pending");
    return { ok: true, tasks };
  },

  ackTask({ agent_id, task_id }) {
    const task = _state.tasks.find(t => t.id === task_id && t.to_agent === agent_id);
    if (!task) throw new Error(`Task ${task_id} not found for ${agent_id}`);
    task.status = "ack";
    task.acked_at = new Date().toISOString();
    saveState();
    return { ok: true, task };
  },

  listAgents() {
    // Mark stale agents as offline
    const now = Date.now();
    for (const a of Object.values(_state.agents)) {
      const age = now - new Date(a.last_heartbeat).getTime();
      a.online = age < HEARTBEAT_TIMEOUT_MS;
    }
    return {
      ok: true,
      agents: Object.values(_state.agents),
      pending_tasks: _state.tasks.filter(t => t.status === "pending").length,
    };
  },

  // Run periodic cleanup of old tasks
  _gc({ max_age_hours = 24 } = {}) {
    const cutoff = Date.now() - max_age_hours * 3600 * 1000;
    const before = _state.tasks.length;
    _state.tasks = _state.tasks.filter(t => new Date(t.created_at).getTime() > cutoff);
    saveState();
    return { ok: true, removed: before - _state.tasks.length };
  },
};

export default skill;
