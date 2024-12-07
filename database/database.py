import motor.motor_asyncio
from config import DB_URI, DB_NAME

# MongoDB setup
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

# Default verify status
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

# Function to create a new user document template
def new_user(id):
    return {
        '_id': id,
        'verify_status': default_verify.copy(),  # Use a copy to avoid modifying default_verify
        'premium_status': {'has_premium': False}  # Ensure premium_status is part of the new user
    }

# Check if a user is present in the database
async def present_user(user_id: int):
    try:
        found = await user_data.find_one({'_id': user_id})
        return bool(found)
    except Exception as e:
        print(f"Error checking user presence: {e}")
        return False

# Add a new user to the database
async def add_user(user_id: int):
    try:
        user = new_user(user_id)
        await user_data.insert_one(user)
    except Exception as e:
        print(f"Error adding user: {e}")

# Retrieve verify status for a user
async def db_verify_status(user_id):
    try:
        user = await user_data.find_one({'_id': user_id})
        if user:
            return user.get('verify_status', default_verify)
        return default_verify
    except Exception as e:
        print(f"Error retrieving verify status: {e}")
        return default_verify

# Update verify status for a user
async def db_update_verify_status(user_id, verify):
    try:
        await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})
    except Exception as e:
        print(f"Error updating verify status: {e}")

# Retrieve a list of all user IDs in the database
async def full_userbase():
    try:
        user_docs = user_data.find()
        user_ids = [doc['_id'] async for doc in user_docs]
        return user_ids
    except Exception as e:
        print(f"Error retrieving full userbase: {e}")
        return []

# Delete a user from the database
async def del_user(user_id: int):
    try:
        await user_data.delete_one({'_id': user_id})
    except Exception as e:
        print(f"Error deleting user: {e}")

# Check if user has premium status (default to False if user doesn't exist)
# Check if user has premium status (default to False if user doesn't exist)
async def is_premium(user_id: int):
    try:
        # Fetch the user from the database
        user = await user_data.find_one({'_id': user_id})

        # Debugging: print user document
        print(f"Fetched user: {user}")

        # If user is found, return the value of 'has_premium', else return False
        if user:
            return user.get('premium_status', {}).get('has_premium', False)
        return False
    except Exception as e:
        print(f"Error checking premium status: {e}")
        return False


# Add premium status to a user
async def add_premium(user_id: int):
    try:
        # Ensure the user exists
        if not await present_user(user_id):
            await add_user(user_id)

        # Update the user's premium status
        await user_data.update_one(
            {'_id': user_id},
            {'$set': {'premium_status.has_premium': True}}
        )
    except Exception as e:
        print(f"Error adding premium status: {e}")

# Remove premium status from a user
async def remove_premium(user_id: int):
    try:
        await user_data.update_one(
            {'_id': user_id},
            {'$set': {'premium_status.has_premium': False}}
        )
    except Exception as e:
        print(f"Error removing premium status: {e}")
