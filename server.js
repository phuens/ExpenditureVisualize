import express from 'express';
import { join } from 'path';
import serveStatic from 'serve-static';

const app = express();
app.use(serveStatic(join(__dirname, 'dist')));

const port = process.env.PORT || 8000;
app.listen(port);
console.log(`server started ${port}`);
