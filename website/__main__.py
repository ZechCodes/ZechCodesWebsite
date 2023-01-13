import uvicorn
from website.app import app
import copy


logging_config = copy.deepcopy(uvicorn.config.LOGGING_CONFIG)
logging_config["formatters"]["default"]["fmt"] = "WEB: %(levelprefix)s %(message)s"


uvicorn.run(app, host="0.0.0.0", port=8000, log_config=logging_config)