const mongoose = require("mongoose")
const { Schema } = require("mongoose")
const Subscriber = require("./subscriber")
const passportLocalMongoose = require("passport-local-mongoose")
const userSchema = new Schema(
    {
        name:{
            type: String,
            required: true,
            trim: true
        },
        email: {
            type: String,
            required: true,
            lowercase: true,
            trim: true,
            unique: true

        },
        sex: {
            type: String,
            required: true,
            enum : ['male','female','unisex'],
        },
        address: {
            type: String,
            required: true,
        },
        tel: {
            type: String,
            required: true,
        },
        password: {
            type: String,
            required: true
        },
        role:{
            enum : ['admin','user']
        }
    },
    {
        timestamps: true
    }
)

userSchema.virtual("fullName").get( function (){
    return `${this.name.first} ${this.name.last}`
})

userSchema.pre("save", function(next){
    let user = this
    if (user.subscribedAccount === undefined) {
        Subscriber.findOne({
            email: user.email
        })
        .then(subscriber => {
            user.subscribedAccount = subscriber
            next()
        })
        .catch(error => {
            console.log(`Error in connecting subscriber: ${error.message}`)
            next(error)
        })
    } else {
        next()
    }
})

userSchema.plugin(passportLocalMongoose,{ usernameField: "email" })

module.exports = mongoose.model("User", userSchema)