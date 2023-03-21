class Database {
  constructor(connection_url, db_name, collection_name){
    this.connection_url = connection_url;
    this.db_name = db_name;
    this.collection_name = collection_name;
   
    this.client = new MongoClient(this.db_name);
    this.connect();
    this.db = this.client.db(this.db_name);
    this.collection = this.db.collection(this.collection_name);
    
  }
  async connect()
  {
    this.client.connect();
  }

  async getUser(filter)
  {    
    return await this.collection.findOne(filter); 
  }

  async insert_one(doc)
  {
    return await this.collection.insertOne(doc);
  }

  async update_one(filter, new_doc)
  {
    return await this.collection.updateOne(filter, new_doc)
  }
}

export default Database;