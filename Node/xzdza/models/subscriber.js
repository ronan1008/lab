const mongoose = require("mongoose")
const { Schema } = mongoose

var subscriberSchema = new Schema(
    {
        name:{
            type: String,
            required: true,
            trim: true
        },
        email: {
            type: String,
            lowercase: true,
            required: true,
            trim: true,
        },
        sex: {
            type: String,
            required: true,
            enum : ['男','女','跨性別'],
        },
        address: {
            type: String,
            required: true,
        },
        birthday: {
            type: Date,
            required: true,
        },
        tel: {
            type: String,
            required: true,
        },
        zodiac: {
            type: String,
            required: true,
            enum : ['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','雞','狗','豬'],
        },
    },
    {
        timestamps: true
    }
)

subscriberSchema.methods.getInfo = function () {
    return `Name: ${this.name} Email: ${this.email} Sex: ${this.sex} address: ${this.address} tel: ${this.tel}`
}

module.exports = mongoose.model("Subscriber", subscriberSchema)