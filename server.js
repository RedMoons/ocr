const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const {spawn} = require('child_process');
const fs = require('fs')

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json({ limit: '15MB' }))

app.post('/', (req, res) => {

    var tmp = Date.now()
    var png = '.png'
    var fileName = tmp+png
    console.log('File name : '+ fileName)

    fs.writeFile(fileName, req.body.imgsource, 'base64', (err) => {
        if (err) throw err
    })
    res.status(200)

    var dataToSend;
    const python = spawn('python3', ['./OcrApi.py',fileName]);
    python.stdout.on('data',  (data) => {
        console.log('Pipe data from python script ...');
        console.log(data)
        console.log(data.toString())
	dataToSend = data.toString();
    });

    python.on('close', (code) => {
        console.log('child process close / return : '+dataToSend); 
	// send data to browser
	res.send(dataToSend)
        setTimeout(() => {  console.log("waiting"); }, 5000);
        var path = '/home/azureuser/fukuNode/'+fileName
	fs.unlink(path, (err) => { 
            if (err) {
                console.error(err)
	        return
            }
	})
        console.log("finished delete image file")
    });


})
app.listen(5000)
