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
const complaints_collection = "complaints"

const user_client = new Database(db_url, db_name, user_collection_name)
const ban_client = new Database(db_url, db_name, ban_collection_name)
const complaints_client = new Database(db_url, db_name, complaints_collection)
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
app.post('/complaints', async function(req ,res) {
  const { email, secretKey } = req.body;
})
app.post('/login', async function (req, res) {
  const { email, password: secretKey } = req.body;
  const user = await user_client.run({email: email}, "find");

  let admin = await admin_client.run({}, 'find');

  if(user.type === "normal" && secretKey === admin.secretKey)
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
  } else if (user.type === "admin" && secretKey === admin.secretKey) {
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

// db interactions for frontend | it's not for api actually i use that section for src/App.svelte!
async function submit_form(email, secretKey)
{
  // EXPRESS_PORT IS DEFINED IN rollup.config.js
  const data = await fetch(`http://localhost:${PORT}/login`, {
    method: "POST",
    body: JSON.stringify({
      email: email,
      password: secretKey
    }),
    headers: {
      "Content-Type": "application/json",
      'Access-Control-Allow-Methods': 'OPTIONS,POST',
      'Access-Control-Allow-Credentials': true,
      'Access-Control-Allow-Origin': '*',
      'X-Requested-With': '*',
    }
  })
  const result = await data.json()

  if (result.response === 200)
  {
    // set stores!
    user_data.set(result.user_data);
    is_logged.set(true)
    page_index.set(1)
    // set variables
    username = result.user_data.username;
    logged = true;
    ui = 1;
    window.alert(`Hoşgeldiniz, ${username}!\nSisteme erişim veriliyor...`)
  } else if(result.response === 403){
    window.alert('ADMIN OLMADIĞINIZ HALDE SİSTEME ERİŞİM\nSAĞLAMAYA ÇALIŞTIĞINIZDAN BANLANIYORSUNUZ.')
    setTimeout(() => window.close(), 2000)
  }
}

async function get_complaints(email, secretKey)
{
 // EXPRESS_PORT IS DEFINED IN rollup.config.js
 const data = await fetch(`http://localhost:${PORT}/login`, {
    method: "POST",
    body: JSON.stringify({
      email: email,
      secretKey: secretKey
    }),
    headers: {
      "Content-Type": "application/json",
      'Access-Control-Allow-Methods': 'OPTIONS,POST',
      'Access-Control-Allow-Credentials': true,
      'Access-Control-Allow-Origin': '*',
      'X-Requested-With': '*',
    }
  });

  const result = await data.json();

  if (result.response === 200)
  {
    return result.data;
  }
}
export { submit_form, get_complaints };
