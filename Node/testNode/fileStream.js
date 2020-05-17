//fs.createWriteStream(path[, options])


let fs = require('fs')

let ws = fs.createWriteStream('./demo.txt',{
            
})

ws.on('open',()=>{
    console.log('stream open')
})

ws.on('close',()=>{
    console.log('stream close')
})

ws.write('馬上放學\n')
ws.write('now\n')
ws.write('好嗎？')
ws.close()



