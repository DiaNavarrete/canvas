from main import app
from model import load_config

if __name__ == '__main__':
    config = load_config()['APP']
    app.run(
       host=config.get("HOST", "{}").format(config['HOST']),
       port=config.get("PORT", config['PORT']))