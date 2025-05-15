# Mock implementation of Firebase services for development
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional


class MockFirestore:
    """
    Mock implementation of Firestore for development.
    Implements a basic in-memory database with collections and documents.
    """
    def __init__(self):
        self._data = {}  # In-memory storage: {collection_name: {doc_id: doc_data}}
        print("Using MockFirestore for development")
        
    def collection(self, collection_name):
        """Get a reference to a collection"""
        if collection_name not in self._data:
            self._data[collection_name] = {}
        return MockCollectionReference(self, collection_name)
        
    def _get_collection(self, collection_name):
        """Internal method to get collection data"""
        return self._data.get(collection_name, {})


class MockCollectionReference:
    """
    Mock implementation of Firestore CollectionReference
    """
    def __init__(self, firestore, collection_name):
        self._firestore = firestore
        self._collection_name = collection_name
        self._query_filters = []
        self._order_by = None
        self._order_direction = None
        self._limit_val = None
        
    def document(self, doc_id=None):
        """Get a document reference"""
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        return MockDocumentReference(self._firestore, self._collection_name, doc_id)
        
    def where(self, field, operator, value):
        """Add a filter to the query"""
        self._query_filters.append((field, operator, value))
        return self
        
    def order_by(self, field, direction="ASCENDING"):
        """Order the query results"""
        self._order_by = field
        self._order_direction = direction
        return self
        
    def limit(self, limit_val):
        """Limit the number of results"""
        self._limit_val = limit_val
        return self
        
    def stream(self):
        """Execute the query and get results"""
        collection_data = self._firestore._get_collection(self._collection_name)
        results = []
        
        # Apply filters
        filtered_data = collection_data.copy()
        for field, op, value in self._query_filters:
            if op == "==":
                filtered_data = {
                    doc_id: doc_data 
                    for doc_id, doc_data in filtered_data.items() 
                    if field in doc_data and doc_data[field] == value
                }
        
        # Convert to document snapshots
        for doc_id, doc_data in filtered_data.items():
            results.append(MockDocumentSnapshot(doc_id, doc_data, self._collection_name, self._firestore))
            
        # Apply ordering if specified
        if self._order_by:
            reverse = self._order_direction == "DESCENDING"
            results.sort(
                key=lambda doc: doc.to_dict().get(self._order_by, ""), 
                reverse=reverse
            )
            
        # Apply limit if specified
        if self._limit_val and len(results) > self._limit_val:
            results = results[:self._limit_val]
            
        return results


class MockDocumentReference:
    """
    Mock implementation of Firestore DocumentReference
    """
    def __init__(self, firestore, collection_name, doc_id):
        self._firestore = firestore
        self._collection_name = collection_name
        self._doc_id = doc_id
        
    def get(self):
        """Get the document data"""
        collection = self._firestore._get_collection(self._collection_name)
        data = collection.get(self._doc_id, None)
        return MockDocumentSnapshot(self._doc_id, data, self._collection_name, self._firestore)
        
    def set(self, data):
        """Set document data"""
        if self._collection_name not in self._firestore._data:
            self._firestore._data[self._collection_name] = {}
        self._firestore._data[self._collection_name][self._doc_id] = data
        return self
        
    def update(self, data):
        """Update document data"""
        if self._collection_name not in self._firestore._data:
            self._firestore._data[self._collection_name] = {}
            
        # Create document if it doesn't exist
        if self._doc_id not in self._firestore._data[self._collection_name]:
            self._firestore._data[self._collection_name][self._doc_id] = {}
            
        # Update fields
        self._firestore._data[self._collection_name][self._doc_id].update(data)
        return self
        
    def delete(self):
        """Delete the document"""
        if self._collection_name in self._firestore._data and self._doc_id in self._firestore._data[self._collection_name]:
            del self._firestore._data[self._collection_name][self._doc_id]
        return self


class MockDocumentSnapshot:
    """
    Mock implementation of Firestore DocumentSnapshot
    """
    def __init__(self, doc_id, data, collection_name, firestore):
        self.id = doc_id
        self._data = data
        self._collection_name = collection_name
        self._firestore = firestore
        self.reference = MockDocumentReference(firestore, collection_name, doc_id)
        
    def to_dict(self):
        """Convert document to dictionary"""
        return self._data if self._data else {}
        
    def exists(self):
        """Check if document exists"""
        return self._data is not None
        
    def get(self, field):
        """Get a field from the document"""
        if not self._data:
            return None
        return self._data.get(field)


class MockStorage:
    """
    Mock implementation of Firebase Storage
    Simulates storing files in memory
    """
    def __init__(self):
        self._files = {}  # {path: {content, contentType}}
        print("Using MockStorage for development")
        
    def blob(self, path):
        """Get a reference to a storage blob"""
        return MockBlob(path, self)


class MockBlob:
    """
    Mock implementation of a Storage Blob
    """
    def __init__(self, path, storage):
        self.path = path
        self._storage = storage
        self.public_url = f"https://storage.example.com/{path}"
        
    def upload_from_string(self, content, content_type=None):
        """Upload content to the blob"""
        self._storage._files[self.path] = {
            "content": content,
            "contentType": content_type
        }
        
    def upload_from_file(self, file_obj, content_type=None):
        """Upload file to the blob"""
        content = file_obj.read()
        self.upload_from_string(content, content_type)
        
    def download_as_string(self):
        """Download blob content as string"""
        if self.path in self._storage._files:
            return self._storage._files[self.path]["content"]
        return None
        
    def delete(self):
        """Delete the blob"""
        if self.path in self._storage._files:
            del self._storage._files[self.path]
            
    def make_public(self):
        """Make the blob publicly accessible"""
        # In mock implementation, all blobs are considered public
        pass


class MockAuth:
    """
    Mock implementation of Firebase Auth
    Simulates user authentication with in-memory storage
    """
    def __init__(self):
        self._users = {}  # {uid: user_data}
        print("Using MockAuth for development")
        
        # Add a default test user
        self.create_user(
            email="test@example.com",
            password="password123",
            display_name="Test User"
        )
        
    def create_user(self, **kwargs):
        """Create a new user"""
        uid = kwargs.get("uid", str(uuid.uuid4()))
        user_data = {
            "uid": uid,
            "email": kwargs.get("email"),
            "email_verified": kwargs.get("email_verified", False),
            "display_name": kwargs.get("display_name"),
            "photo_url": kwargs.get("photo_url"),
            "disabled": kwargs.get("disabled", False),
            "password": kwargs.get("password", "password123"),  # Not stored in real Firebase
            "created_at": datetime.now()
        }
        self._users[uid] = user_data
        return MockUserRecord(user_data)
        
    def get_user(self, uid):
        """Get user by UID"""
        if uid in self._users:
            return MockUserRecord(self._users[uid])
        raise ValueError(f"No user with UID: {uid}")
        
    def get_user_by_email(self, email):
        """Get user by email"""
        for user in self._users.values():
            if user["email"] == email:
                return MockUserRecord(user)
        raise ValueError(f"No user with email: {email}")
        
    def update_user(self, uid, **kwargs):
        """Update user data"""
        if uid in self._users:
            # Map kwargs from Firebase format to our mock format
            if "displayName" in kwargs:
                kwargs["display_name"] = kwargs.pop("displayName")
            if "photoURL" in kwargs:
                kwargs["photo_url"] = kwargs.pop("photoURL")
            if "emailVerified" in kwargs:
                kwargs["email_verified"] = kwargs.pop("emailVerified")
                
            # Update user data
            self._users[uid].update(kwargs)
            return MockUserRecord(self._users[uid])
        raise ValueError(f"No user with UID: {uid}")
        
    def delete_user(self, uid):
        """Delete a user"""
        if uid in self._users:
            del self._users[uid]
        else:
            raise ValueError(f"No user with UID: {uid}")
            
    def verify_id_token(self, token):
        """
        Verify a Firebase ID token
        For mock implementation, we'll accept any non-empty string as a valid token
        and assume it contains the UID as the token value
        """
        if not token:
            raise ValueError("Invalid token")
            
        # If token is a UID in our system, use it directly
        if token in self._users:
            return {"uid": token}
            
        # Otherwise, use the first user we have
        if self._users:
            first_uid = next(iter(self._users.keys()))
            return {"uid": first_uid}
            
        # If no users, create a test user
        test_uid = str(uuid.uuid4())
        self.create_user(
            uid=test_uid,
            email="test@example.com",
            display_name="Test User"
        )
        return {"uid": test_uid}


class MockUserRecord:
    """
    Mock implementation of a Firebase UserRecord
    """
    def __init__(self, user_data):
        self.uid = user_data.get("uid")
        self.email = user_data.get("email")
        self.email_verified = user_data.get("email_verified", False)
        self.display_name = user_data.get("display_name")
        self.photo_url = user_data.get("photo_url")
        self.disabled = user_data.get("disabled", False)
        self.custom_claims = user_data.get("custom_claims", {})
        self.created_at = user_data.get("created_at", datetime.now())
        self.last_sign_in_at = user_data.get("last_sign_in_at")
        
    def __str__(self):
        return f"User(uid={self.uid}, email={self.email}, display_name={self.display_name})"
