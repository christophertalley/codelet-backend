# Backend Routes

1. Users:
   - POST "/users"
     - This endpoint will create a new user
   - PUT "/users/:user_id"
     - This endpoint will update user information
 
2. Categories
    - GET "/categories"
      - This endpoint will be used to get all of the categories
    - GET "/categories/:category_id"
      - This endpoint will be used to get a single category and its sets
    - PUT "/categories/:category_id"

3. Flash Cards:
   - GET "/flashcard/:id"
     - This endpoint returns all info for a single flashcard @id
   - POST "/flashcard/new"
     - This endpoint created a new flashcard
     - updates flashcardset
   - PUT "/flashcard/:id/update"
     - This endpoint updates an existing flashcard @id
     - updates flashcardset
   - DELETE "/flashcard/:id/delete"
     - This endpoint deletes an existing flashcard @id
     - updates flashcardset to remove from set

4. Flash Card Sets:
   - GET "/sets"
     - This endpoint returns all sets with category, vote, and favorite info
   - GET "/sets/:id"
     - This endpoint returns all flashcards in a set @id
   - POST "/sets/new"
     - This endpoint creates a new set
   - PUT "/sets/:id/update"
     - This endpoint updates an existing set @id
   - DELETE "/sets/:id/delete"
     - This endpoint deletes an existing set @id
     - deletes all flashcards, votes, comments, favorites on that set