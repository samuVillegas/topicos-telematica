
const express = require('express')
const app = express()
const morgan = require('morgan')
require('dotenv').config()

//Importamos los métodos de grpc
const { listFiles: listFilesGrpc, getFile: getFileGrpc } = require('./grpc/methods');
const { listFiles: ListFilesMom, getFile: getFileMom } = require('./mom/methods');

//Middlewares
app.use(morgan('dev'))
app.set('grpc', true)


app.get('/', (req, res) => {
    res.send('Welcome API')
})

app.get('/list_files', async (req, res) => {
    if (app.get('grpc')) {
        app.set('grpc', false);
        //Send messages with grpc
        const data = await listFilesGrpc();
        return res.send(data.message)

    } else {
        app.set('grpc', true);
        //Send messages with MOM
        const data = await ListFilesMom();
        return res.send(data)
    }
})

app.get('/find_file/:name', async (req, res) => {
    if (app.get('grpc')) {
        app.set('grpc', false);
        //Send messages with grpc
        const data = await getFileGrpc(req.params.name);
        return res.send(data.message)
    } else {
        app.set('grpc', true);
        //Send messages with MOM
        const data = await getFileMom(req.params.name);
        return res.send(data)
    }
})

app.listen(process.env.PORT, () => {
    console.log(`Example app listening on port ${process.env.PORT}`)
})
