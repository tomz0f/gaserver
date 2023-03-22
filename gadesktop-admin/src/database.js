const {MongoClient} = require('mongodb');

class Database {
  constructor(connection_url, db_name, collection_name){
    this.connection_url = connection_url;
    this.db_name = db_name;
    this.collection_name = collection_name;

    this.client = new MongoClient(this.connection_url);
    this.connect();
    this.db = this.client.db(this.db_name);
    this.collection = this.db.collection(this.collection_name);

  }

  change_collection(collection_name)
  {
    this.collection_name = collection_name;
    this.collection = this.db.collection(collection_name);
  }

  async delete_user(filter)
  {
    await this.collection.deleteOne(filter);
  }


  async connect()
  {
    this.client.connect();
  }

  async getUser(filter)
  {
    let x = await this.collection.findOne(filter);
    return x;
  }

  async create_banned_account(doc)
  {
    let x = await this.collection.insertOne(doc);
    return x;
  }

  async update_one(filter, new_doc)
  {
    let x = await this.collection.updateOne(filter, new_doc)
    return x;
  }
}

module.exports = { Database };
