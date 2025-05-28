const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const { spawn } = require("child_process");

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: "*" } });

io.on("connection", (socket) => {
  console.log("Client connected");
  socket.on("query", (msg) => {
    const process = spawn("python", ["../ai/rag_engine/query_rag.py"]);
    process.stdin.write(msg + "\n");
    process.stdin.end();
    process.stdout.on("data", (data) => {
      socket.emit("response", data.toString());
    });
  });
});

httpServer.listen(3001, () => console.log("WS Server running on port 3001"));