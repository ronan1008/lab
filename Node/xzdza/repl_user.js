const mongoose = require("mongoose")
const User = require("./models/user")

let mongoDbAtlas = "mongodb+srv://xzdzaorgtw:886229936810@xzdza.elxrf.mongodb.net/xzdza?retryWrites=true&w=majority"
//let mongoDB = "mongodb://localhost:27017/xzdza"

mongoose.connect(mongoDbAtlas, 
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
