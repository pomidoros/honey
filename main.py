import os

import uvicorn

from app.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8084")), log_config=None)
