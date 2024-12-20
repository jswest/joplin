import { spawn } from "child_process";
import { app, BrowserWindow } from "electron";
import { dirname, join } from "path";
import kill from "tree-kill";
import { fileURLToPath } from "url";

let mainWindow;
let fastApiProcess;
let chromaProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:5173");
  } else {
    mainWindow.loadFile(
      join(dirname(fileURLToPath(import.meta.url)), "build", "index.html")
    );
  }
}

function startBackendProcesses() {
  const venv =
    process.env.NODE_ENV === "development"
      ? join(dirname(fileURLToPath(import.meta.url)), ".venv")
      : join(process.resourcesPath, "venv");
  const pythonPath = join(venv, "bin", "python");
  const chromaPath = join(venv, "bin", "chroma");

  fastApiProcess = spawn(
    pythonPath,
    ["-m", "uvicorn", "api.main:app", "--port", "8001"],
    {
      stdio: "pipe",
      shell: true,
      env: {
        ...process.env,
        VIRTUAL_ENV: venv,
        PATH: `${join(venv, "bin")}:${process.env.PATH}`,
      },
    }
  );

  fastApiProcess.stdout.on("data", (data) => {
    console.log(`FastAPI: ${data}`);
  });

  fastApiProcess.stderr.on("data", (data) => {
    console.error(`FastAPI Error: ${data}`);
  });

  chromaProcess = spawn(chromaPath, ["run", "--path", "./db/chroma"], {
    stdio: "pipe",
    shell: true,
    env: {
      ...process.env,
      VIRTUAL_ENV: venv,
      PATH: `${join(venv, "bin")}:${process.env.PATH}`,
    },
  });

  chromaProcess.stdout.on("data", (data) => {
    console.log(`Chroma: ${data}`);
  });

  chromaProcess.stderr.on("data", (data) => {
    console.error(`Chroma Error: ${data}`);
  });
}

app.whenReady().then(() => {
  startBackendProcesses();
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", async () => {
  const killProcess = (process, name) => {
    return new Promise((resolve) => {
      if (!process) {
        resolve();
        return;
      }

      kill(process.pid, "SIGTERM", (err) => {
        if (err) {
          console.error(`Error killing ${name}:`, err);
        } else {
          console.log(`${name} terminated successfully`);
        }
        resolve();
      });
    });
  };

  await Promise.all([
    killProcess(fastApiProcess, "FastAPI"),
    killProcess(chromaProcess, "Chroma"),
  ]);
});
