//引入 subscriber module
const Subscriber = require("../models/subscriber")


// //從database 導出 getAllSubscribers
// //getAllSubscribers pass資料至下一個中間件函式
// exports.getAllSubscribers = (req, res, next) => {
//     //在 Subscriber model 用 find 查詢
//     Subscriber.find( {}, (error, subscribers) =>{
//         //將錯誤pass到下一個中間件函式
//         if(error) next(error)
//         //在request 物件，設定從Mongo DB返回的資料
//         req.data = subscribers
//         //繼續下一個中間件函式
//         next()
//     }) 
// }

exports.getAllSubscribers = (req, res) =>{
    Subscriber.find({})
        .exec()
        .then(subscribers =>{
            res.render("subscribers",{subscribers: subscribers})
        })
        .catch(error =>{
            console.log(error.message)
            return [];
        })
        .then(() =>{
            console.log("promise complete")
        })
}       




//新增一個 action 用來呈現 contact頁面
exports.getSubscriptionPage = (req, res) => {
	res.render("contact")
}

// //新增一個 action 儲存 subscribers
// exports.saveSubscriber = (req,res) => {
    
// 	//產生一個新的 subscriber
// 	let newSubscriber = new Subscriber({
// 		name: req.body.name,
// 		email: req.body.email,
// 		zipCode: req.body.zipCode
// 	})

// 	//儲存這個 subscriber
// 	newSubscriber.save((error, result) => {
// 		if (error) res.send(error)
// 		res.render("thanks")
// 	})
// }


exports.saveSubscriber = (req, res) => {
    let newSubscriber = new Subscriber({
        name: req.body.name,
        email: req.body.email,
        zipCode: req.body.zipCode
    })
    newSubscriber
        .save()
        .then( result => {
            res.render("thanks")
        })
        .catch(error => {
            if(error) res.send(error)
        })
}
