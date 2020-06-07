from dotenv import load_dotenv
load_dotenv()

from app import app, db  # noqa
from app.models import User, Category, Set, Card  # noqa

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(nickname="demo", email="demo@demo.com")
    cat1 = Category(name="Category 1")
    cat2 = Category(name="Category 2")
    set1 = Set(
        title="Set 1",
        description="Set 1 description",
        category_id=1,
        user_id=1,
        created_at="2020-06-06 16:56:54.271262"
    )
    set2 = Set(
        title="Set 2",
        description="Set 2 description",
        category_id=2,
        user_id=1,
        created_at="2020-06-06 16:56:54.271262"
    )
    card1 = Card(
        term="card1",
        definition="card def1",
        set_id=1
    )
    card2 = Card(
        term="card2",
        definition="card def2",
        set_id=1
    )
    card3 = Card(
        term="card3",
        definition="card def3",
        set_id=1
    )
    card4 = Card(
        term="card4",
        definition="card def4",
        set_id=1
    )
    card5 = Card(
        term="card5",
        definition="card def5",
        set_id=1
    )
    card6 = Card(
        term="card1",
        definition="card def1",
        set_id=2
    )
    card7 = Card(
        term="card2",
        definition="card def2",
        set_id=2
    )

    db.session.add(user1)
    db.session.add(user1)
    db.session.add(user1)
    db.session.add(user1)
    db.session.add(user1)
    db.session.add(user1)
    db.session.add(cat1)
    db.session.add(cat2)
    db.session.add(set1)
    db.session.add(set2)
    db.session.add(card1)
    db.session.add(card2)
    db.session.add(card3)
    db.session.add(card4)
    db.session.add(card5)
    db.session.add(card6)
    db.session.add(card7)
    db.session.commit()
