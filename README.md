# Desarrollo-Back-End 
# Express.js Backend

Backend escalable y mantenible construido con **Node.js** y **Express.js**.

Este proyecto utiliza una arquitectura modular que separa las rutas, controladores, modelos, middlewares, servicios, utilidades y configuración de la aplicación.

---

# Estructura del proyecto

```text
project/
│
├── src/
│   │
│   ├── controllers/
│   │   ├── user.controller.js
│   │   ├── auth.controller.js
│   │   └── product.controller.js
│   │
│   ├── models/
│   │   ├── user.model.js
│   │   └── product.model.js
│   │
│   ├── routes/
│   │   ├── user.routes.js
│   │   ├── auth.routes.js
│   │   └── product.routes.js
│   │
│   ├── middlewares/
│   │   ├── auth.middleware.js
│   │   ├── error.middleware.js
│   │   └── upload.middleware.js
│   │
│   ├── services/
│   │   ├── user.service.js
│   │   └── auth.service.js
│   │
│   ├── utils/
│   │   ├── generateToken.js
│   │   ├── asyncHandler.js
│   │   └── apiResponse.js
│   │
│   ├── config/
│   │   ├── db.js
│   │   └── env.js
│   │
│   ├── validators/
│   │   ├── user.validator.js
│   │   └── auth.validator.js
│   │
│   ├── app.js
│   └── server.js
│
├── .env
├── .env.example
├── .gitignore
├── package.json
├── package-lock.json
└── README.md
```

---

# Responsabilidad de cada carpeta

## `controllers/`

Los controllers contienen la lógica encargada de recibir las solicitudes HTTP y enviar las respuestas.

```js
export const getUsers = async (req, res) => {
  const users = await User.find();

  res.status(200).json({
    success: true,
    users,
  });
};
```

La idea principal es:

```text
Request → Controller → Response
```

El controller debería encargarse principalmente de la comunicación HTTP y evitar contener toda la lógica de negocio.

---

## `models/`

Los models representan la estructura de los datos almacenados en la base de datos.

Por ejemplo, utilizando MongoDB y Mongoose:

```js
import mongoose from "mongoose";

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },

    email: {
      type: String,
      required: true,
      unique: true,
    },

    password: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

export default mongoose.model("User", userSchema);
```

Piensa en:

```text
Model = Cómo se estructura la información
```

---

## `routes/`

Las routes definen los endpoints de nuestra API.

```js
import express from "express";
import { getUsers } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/", getUsers);

export default router;
```

Luego podemos registrar las rutas en `app.js`:

```js
import userRoutes from "./routes/user.routes.js";

app.use("/api/users", userRoutes);
```

Ahora:

```text
GET /api/users
```

ejecutará:

```text
user.routes.js
      ↓
user.controller.js
```

---

## `middlewares/`

Los middlewares son funciones que se ejecutan durante el procesamiento de una solicitud.

Se utilizan comúnmente para:

* Autenticación
* Autorización
* Validación
* Manejo de errores
* Upload de archivos
* Logging
* Procesamiento de requests

Ejemplo:

```js
export const protect = async (req, res, next) => {
  // Verificar token

  // Obtener usuario
  req.user = user;

  next();
};
```

La función:

```js
next();
```

le indica a Express que continúe con el siguiente middleware o controller.

---

## `services/`

Los services contienen la lógica de negocio de la aplicación.

Esta carpeta es especialmente útil cuando el proyecto comienza a crecer.

```js
export const createUser = async (userData) => {
  const existingUser = await User.findOne({
    email: userData.email,
  });

  if (existingUser) {
    throw new Error("El usuario ya existe");
  }

  const user = await User.create(userData);

  return user;
};
```

El controller puede mantenerse sencillo:

```js
export const register = async (req, res) => {
  const user = await createUser(req.body);

  res.status(201).json({
    success: true,
    user,
  });
};
```

Una forma sencilla de recordarlo:

```text
Controller = HTTP
Service    = Lógica de negocio
Model      = Base de datos
```

---

## `utils/`

La carpeta `utils` contiene funciones auxiliares y reutilizables.

```text
utils/
├── generateToken.js
├── asyncHandler.js
├── apiResponse.js
├── pagination.js
└── formatDate.js
```

Ejemplo:

```js
export const generateToken = (userId) => {
  return jwt.sign(
    { id: userId },
    process.env.JWT_SECRET,
    {
      expiresIn: "7d",
    }
  );
};
```

La idea es evitar repetir código que puede reutilizarse en diferentes partes de la aplicación.

---

## `config/`

Aquí colocamos la configuración de nuestra aplicación.

Por ejemplo, la conexión a MongoDB:

```js
import mongoose from "mongoose";

export const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);

    console.log("Base de datos conectada");
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
};
```

Podríamos tener:

```text
config/
├── db.js
├── env.js
└── cloudinary.js
```

---

## `validators/`

Los validators se encargan de comprobar que los datos enviados por el cliente tengan el formato correcto.

Ejemplo utilizando Zod:

```js
import { z } from "zod";

export const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(6),
});
```

Esto permite evitar que información incorrecta llegue a nuestra lógica de negocio.

---

# Flujo de una Request

Una solicitud normalmente sigue este flujo:

```text
                    HTTP Request
                         │
                         ▼
                       Route
                         │
                         ▼
                     Middleware
                         │
                         ▼
                     Controller
                         │
                         ▼
                       Service
                         │
                         ▼
                        Model
                         │
                         ▼
                      Database
                         │
                         ▼
                       Service
                         │
                         ▼
                     Controller
                         │
                         ▼
                    HTTP Response
```

Por ejemplo:

```text
POST /api/users
       │
       ▼
user.routes.js
       │
       ▼
auth.middleware.js
       │
       ▼
user.controller.js
       │
       ▼
user.service.js
       │
       ▼
user.model.js
       │
       ▼
    MongoDB
```

---

# Instalación

Clona el proyecto:

```bash
git clone <repository-url>

cd project
```

Instala las dependencias:

```bash
npm install
```

Crea el archivo `.env`:

```bash
touch .env
```

Ejemplo:

```env
PORT=5000

MONGO_URI=mongodb://localhost:27017/my_database

JWT_SECRET=your_secret_key
```

---

# Ejecutar el servidor

Para desarrollo:

```bash
npm run dev
```

Para producción:

```bash
npm start
```

Ejemplo de `package.json`:

```json
{
  "scripts": {
    "dev": "nodemon src/server.js",
    "start": "node src/server.js"
  }
}
```

---

# `server.js`

El archivo `server.js` es el encargado de iniciar el servidor.

```js
import app from "./app.js";

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en el puerto ${PORT}`);
});
```

---

# `app.js`

`app.js` contiene la configuración principal de Express.

```js
import express from "express";

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    message: "API funcionando correctamente",
  });
});

export default app;
```

---

# Variables de entorno

Nunca debemos subir el archivo `.env` a GitHub.

Nuestro `.gitignore` debería contener:

```text
node_modules/
.env
```

En su lugar, podemos crear:

```text
.env.example
```

Con:

```env
PORT=

MONGO_URI=

JWT_SECRET=
```

El archivo `.env.example` sirve para mostrar qué variables necesita el proyecto sin revelar información privada.

---

# Ejemplo de API

### Usuarios

| Método | Endpoint         | Descripción                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/users`     | Obtener todos los usuarios |
| GET    | `/api/users/:id` | Obtener un usuario         |
| POST   | `/api/users`     | Crear un usuario           |
| PATCH  | `/api/users/:id` | Actualizar un usuario      |
| DELETE | `/api/users/:id` | Eliminar un usuario        |

---

# Ejemplo de arquitectura

Para una funcionalidad de usuarios:

```text
routes
   │
   └── user.routes.js
           │
           ▼
controllers
   │
   └── user.controller.js
           │
           ▼
services
   │
   └── user.service.js
           │
           ▼
models
   │
   └── user.model.js
           │
           ▼
       Database
```

Esta separación permite que el proyecto sea más fácil de:

* Mantener
* Testear
* Depurar
* Escalar
* Desarrollar en equipo

---

# Dependencias recomendadas

Para una API básica:

```bash
npm install express dotenv cors
```

Para MongoDB:

```bash
npm install mongoose
```

Para autenticación:

```bash
npm install jsonwebtoken bcrypt
```

Para validación:

```bash
npm install zod
```

Para desarrollo:

```bash
npm install -D nodemon
```

---

# Buenas prácticas

## Mantener los controllers pequeños

Evita colocar toda la lógica dentro del controller.

Evitar:

```text
Controller
 ├── Validación
 ├── Queries de base de datos
 ├── Autenticación
 ├── Lógica de negocio
 ├── Procesamiento de archivos
 └── Response
```

Preferir:

```text
Controller
    ↓
Service
    ↓
Model
    ↓
Database
```

---

# Una responsabilidad por capa

```text
Routes       → Definen endpoints
Middleware   → Procesan requests
Controllers  → Manejan HTTP
Services     → Contienen lógica de negocio
Models       → Manejan datos
Utils        → Funciones reutilizables
Config       → Configuración
Validators   → Validación de datos
```

---

# Arquitectura para proyectos grandes

Cuando el proyecto comienza a crecer considerablemente, podemos pasar de una arquitectura basada en carpetas globales a una arquitectura basada en features o módulos:

```text
src/
│
├── modules/
│   │
│   ├── users/
│   │   ├── user.controller.js
│   │   ├── user.model.js
│   │   ├── user.routes.js
│   │   ├── user.service.js
│   │   └── user.validator.js
│   │
│   ├── auth/
│   │   ├── auth.controller.js
│   │   ├── auth.service.js
│   │   ├── auth.routes.js
│   │   └── auth.validator.js
│   │
│   └── products/
│       ├── product.controller.js
│       ├── product.model.js
│       ├── product.routes.js
│       └── product.service.js
│
├── middlewares/
├── utils/
├── config/
├── app.js
└── server.js
```

Esto permite que cada funcionalidad tenga todo lo relacionado con ella en un mismo lugar.

Por ejemplo:

```text
users/
├── user.controller.js
├── user.model.js
├── user.routes.js
├── user.service.js
└── user.validator.js
```

en lugar de tener todos los controllers, models, routes y services del proyecto separados globalmente.

---

# Resumen

La arquitectura básica:

```text
                Express API
                    │
            ┌───────┴───────┐
            │               │
          Routes        Middlewares
            │               │
            └───────┬───────┘
                    ▼
               Controllers
                    │
                    ▼
                 Services
                    │
                    ▼
                  Models
                    │
                    ▼
                Database
```

La idea principal es **no crear carpetas solamente porque son "estándar"**.

Para un proyecto pequeño, puedes comenzar con:

```text
src/
├── controllers/
├── models/
├── routes/
├── middlewares/
├── utils/
├── config/
├── app.js
└── server.js
```

A medida que el proyecto crezca, puedes incorporar:

```text
services/
validators/
modules/
```

La arquitectura debe crecer junto con la aplicación, no al revés.
