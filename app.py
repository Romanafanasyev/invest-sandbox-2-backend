from routes import app
from models import Base
from sqlalchemy import create_engine

if __name__ == '__main__':
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)
    app.run(debug=True)
