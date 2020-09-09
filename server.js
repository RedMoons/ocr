const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const {spawn} = require('child_process');
const fs = require('fs')

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json({ limit: '15MB' }))

app.post('/', (req, res) => {
    fs.writeFile('./out.png', req.body.imgsource, 'base64', (err) => {
        if (err) throw err
    })
    res.status(200)

    var dataToSend;
    const python = spawn('python3', ['./OcrApi.py']);
    python.stdout.on('data',  (data) => {
        console.log('Pipe data from python script ...');
        console.log(data)
        console.log(data.toString())
	dataToSend = data.toString();
    });

    python.on('close', (code) => {
         console.log('child process close all stdio with code $code');
	 
	 
	 // send data to browser
	 res.send(dataToSend)
    });

})
app.listen(5000)
