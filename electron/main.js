const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let pyProc = null;
let mainWindow = null;

function startFlask() {
  return new Promise((resolve) => {
    const script = path.join(__dirname, "..", "app.py"); 
    console.log("Starting Flask from:", script);
    
    pyProc = spawn("python", [script]);
    
    pyProc.stdout.on("data", (data) => {
      console.log(`Flask: ${data}`);
      if (data.includes("Running on") || data.includes("Debugger PIN")) {
        console.log("Flask is ready!");
        resolve(true);
      }
    });

    pyProc.stderr.on("data", (data) => {
      console.error(`Flask error: ${data}`);
    });

    setTimeout(() => {
      console.log("Using fallback timeout");
      resolve(true);
    }, 5000);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  startFlask().then(() => {
    console.log("Loading URL...");
    mainWindow.loadURL("http://localhost:5000");

    mainWindow.webContents.openDevTools();
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (pyProc) pyProc.kill();
  if (process.platform !== "darwin") app.quit();
});