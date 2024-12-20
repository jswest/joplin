import { spawn } from "child_process";

async function setup() {
  const create = spawn("python3", ["-m", "venv", ".venv"], {
    stdio: "inherit",
    shell: true,
  });

  await new Promise((resolve, reject) => {
    create.on("exit", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Failed to create venv, exit code: ${code}`));
      }
    });
  });

  const install = spawn(
    ".venv/bin/pip",
    ["install", "-r", "requirements.txt"],
    {
      stdio: "inherit",
      shell: true,
    }
  );

  await new Promise((resolve, reject) => {
    install.on("exit", (code) => {
      if (code === 0) resolve();
      else
        reject(new Error(`Failed to install requirements, exit code: ${code}`));
    });
  });
}

setup().catch(console.error);
