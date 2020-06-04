const express = require('express')
//使用模板引擎
const expressHandlebars = require('express-handlebars')
const app = express()
const fortune = require('./lib/fortune')

app.use(express.static(__dirname + '/public'))

//設定模板引擎
app.engine('handlebars', expressHandlebars({
    defaultLayout: 'main',
}))
app.set('view engine','handlebars')

const port = process.env.PORT || 3000
app.get('/', (req, res)=>{
    res.render('home')
})

const fortunes = [
    "Conquer your fears or they will conquer you.",
    "Rivers need springs.",
    "Do not fear what you don't know.",
    "You will have a pleasant surprise.",
    "Whenever possible, keep it simple.",
]

app.get('/about', (req, res)=>{
    res.render('about',{ fortune: fortune.getFortune()})
})


//custom 404 page
//app.use 是一個中間件
app.use((req, res)=>{
    res.status(404)
    res.render('404')
})

//custom 500 page

app.use((err, req, res, next)=>{
    console.error(err.message)
    res.status(500)
    res.render('500')
})

app.listen(port, ()=> console.log(
    `Express started on http://localhost:${port};` + 
    `press ctrl-c to terminate.`))

