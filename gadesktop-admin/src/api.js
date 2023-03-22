const express = require('express');
const bodyParser = require('body-parser');
const { is_logged } = require('./stores');
const cors = require('cors');
const { Database } = require('./database');

require('dotenv').config();
const PORT = process.env.EXPRESS_PORT;
const db_url = process.env.DB_URI;

const db_name = "galbul";
const user_collection_name = "users";
const ban_collection_name = "banned_emails";

const user_client = new Database(db_url, db_name, user_collection_name)
const ban_client = new Database(db_url, db_name, ban_collection_name)
const admin_client = new Database(db_url, db_name, process.env.ADMIN_DB_COLLECTION)

// const database = new Database(db_url, db_name, user_collection);
// await database.client.connect();


const app = express();
app.use(cors())
app.use(bodyParser.json());

app.get('/logout', function (req, res) {
  is_logged.set(false)

  res.status(200).json({
    message: "LOGOUT_SUCCESS",
    response: 200
  })
})

app.post('/login', async function (req, res) {
  const { email, password } = req.body;
  const user = await user_client.run({email: email}, "find");

  let admin = await admin_client.run({}, 'find');
  if(user.type === "normal" && password === admin.secretKey)
  {
    user_client.deleteOne({
      "email": user.email
    }, "delete")

    ban_client.run({
      "email": user.email
    }, "insert")
    
    return res.status(403).json({
      message: "BANNING_THIS_USER_PERMENANTLY_FOR_HACKING_CRIME",
      response: 403,
      user: null
    })
  } else if (user.type === "admin" && password === admin.secretKey) {
      isLogged.set(true)

      return res.status(200).json({
        message: "AUTHORIZED",
        response: 200,
        user_data: user
      });
  } else {
    res.status(500).json({
      message: "LOGIN_FAILURE",
      response: 500,
    })
  }
});

app.listen(PORT, () => console.log(`[SERVER] AT http://localhost:${PORT}/`))