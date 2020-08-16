const mongoose = require("mongoose")
const User = require("./models/user")

mongoose.connect("mongodb://localhost:27017/xzdza", 
                    {
                        useNewUrlParser: true,
                        useUnifiedTopology: true,
                        useCreateIndex: true,
                        useFindAndModify: false
                    }
                )
User.deleteMany({})
    .then((items) => console.log(`Removed ${items.n} records`))
    .then(() => { 
        body = {
            name:"shock lee",
            loginId: "xzdza",
            email:"ronan1008@yahoo.com.tw",
            sex:"male",
            address:"new taipei city",
            tel:0937844405,
            password:'123456',
            role:"admin"
        }
        let newUser = new User(body)
        return User.create(body)



    })
	.then( admin => {
		console.log(`Created Admin: ${admin.loginId}`)
	})
