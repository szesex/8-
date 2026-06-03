// skills/interclaw_worker.js
// Single worker process that connects to the coordinator

import { startInterClawLoop } from "./interclaw_client.js";
import fs from "fs";

const WORKERS_FILE = "/home/node/.openclaw/workspace/state/workers.json";
const TARGET_AGENT = process.argv[2]; // e.g., "claw_trading_002"

if (!TARGET_AGENT) {
  console.error("Usage: node interclaw_worker.js <agent_id>");
  process.exit(1);
}

const { workers } = JSON.parse(fs.readFileSync(WORKERS_FILE, "utf-8"));
const worker = workers.find(w => w.agent_id === TARGET_AGENT);
if (!worker) {
  console.error(`Worker ${TARGET_AGENT} not found in ${WORKERS_FILE}`);
  process.exit(1);
}

console.log(`[Worker ${TARGET_AGENT}] Starting...`);

startInterClawLoop({
  agent_id: worker.agent_id,
  skills: worker.skills,
  metadata: worker.metadata,
  onTask: async (task) => {
    console.log(`[Worker ${TARGET_AGENT}] Got task ${task.id} (${task.task_type}) from ${task.from_agent}:`, task.payload);
    // Workers just log for now; in production each worker has its own handler
  },
}).catch(e => {
  console.error(`[Worker ${TARGET_AGENT}] Failed to start:`, e.message);
  process.exit(1);
});
