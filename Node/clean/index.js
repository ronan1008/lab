const express = require('express')
const app = new express()
const ejs = require('ejs')
const mongoose = require('mongoose')
const bodyParser = require('body-parser')
const fileUpload = require('express-fileupload')

const newPostController = require('./controllers/newPost')
const homeController = require('./controllers/home')
const storePostController = require('./controllers/storePost')
const getPostController = require('./controllers/getPost')
const newUserController = require('./controllers/newUser')
const storeUserController = require('./controllers/storeUser')
const loginController = require('./controllers/login')
const loginUserController = require('./controllers/loginUser')
const validateMiddleware = require('./middleware/validateMiddleware')

app.use(express.static('public'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))
app.use(fileUpload())

mongoose.connect('mongodb://localhost/my_database', {useNewUrlParser:true});

app.set('view engine','ejs')


app.listen(4000,()=>{
    console.log('App listening on port 4000')
})
app.get('/',homeController)
app.get('/post/:id',getPostController)
app.post('/posts/store',storePostController)

app.get('/posts/new',newPostController)

const customMiddleWare = (req,res,next)=>{
    console.log('Custom middle ware called')
    next()
}

app.use(customMiddleWare)
app.use('/post/store',validateMiddleware)
app.get('/auth/register',newUserController)
app.post('/users/register',storeUserController)
app.get('/auth/login',loginController);
app.post('/users/login',loginUserController)
