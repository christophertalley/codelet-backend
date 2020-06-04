# Codelet Data Schema

## **User**

| attribute name | data type  |               details |
| -------------- | :--------: | --------------------: |
| id             |  integer   | not null, primary key |
| email          |   string   |      not null, unique |
| username       | string(50) |      not null, unique |

-Associations: User has many sets (one-to-many)

## **Category**

| attribute name | data type  |               details |
| -------------- | :--------: | --------------------: |
| id             |  integer   | not null, primary key |
| name           | string(50) |      not null, unique |

-Associations: Category belongs to many sets (one-to-many)

## **Set**

| attribute name | data type  |               details |
| -------------- | :--------: | --------------------: |
| id             |  integer   | not null, primary key |
| categoryId     | string(50) | not null, foreign key |
| title          |   string   |              not null |
| description    |    text    |                       |
| createdAt      | timestamp  |              not null |

-Associations: Set has many cards (one-to-many) & set has one category (one-to-many)

## **Card**

| attribute name |  data type  |               details |
| -------------- | :---------: | --------------------: |
| id             |   integer   | not null, primary key |
| term           | string(100) |              not null |
| definition     |    text     |              not null |
| setId          |   integer   | foreign key, not null |

-Associations: Card belongs to one set (one-to-many)

## **Favorite**

| attribute name | data type |               details |
| -------------- | :-------: | --------------------: |
| id             |  integer  | not null, primary key |
| setId          |  integer  | not null, foreign key |
| userId         |  integer  | not null, foreign key |

## **Vote**

| attribute name | data type |               details |
| -------------- | :-------: | --------------------: |
| id             |  integer  | not null, primary key |
| setId          |  integer  | not null, foreign key |
| userId         |  integer  | not null, foreign key |
| isUpvote       |  boolean  |                       |