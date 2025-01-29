// import mongoose from "mongoose";

// const MONGODB_URI =
//   process.env.MONGODB_URI ||
//   "mongodb+srv://sagarmanchakatla02:zdVern62hVCbn7ct@cluster0.zehnh.mongodb.net/";

// if (!MONGODB_URI) {
//   throw new Error("Please define the MONGODB_URI environment variable");
// }

// interface MongooseCache {
//   conn: mongoose.Connection | null;
//   promise: Promise<mongoose.Connection> | null;
// }

// let cached: MongooseCache = (global as any).mongoose || {
//   conn: null,
//   promise: null,
// };

// async function dbConnect(): Promise<mongoose.Connection> {
//   if (cached.conn) return cached.conn;

//   if (!cached.promise) {
//     cached.promise = mongoose
//       .connect(MONGODB_URI, {
//         useNewUrlParser: true,
//         useUnifiedTopology: true,
//       })
//       .then((mongoose) => mongoose.connection);
//   }

//   cached.conn = await cached.promise;
//   return cached.conn;
// }

// export default dbConnect;

// import { MongoClient } from "mongodb";
//   "mongodb+srv://sagarmanchakatla02:zdVern62hVCbn7ct@cluster0.zehnh.mongodb.net/";

import mongoose from "mongoose";
const URI =
  "mongodb+srv://sagarmanchakatla02:zdVern62hVCbn7ct@cluster0.zehnh.mongodb.net/";

type ConnectionObect = {
  isConnected?: number;
};

const connection: ConnectionObect = {};

async function dbConnect(): Promise<void> {
  if (connection.isConnected) {
    console.log("MongoDB is already connected");
    return;
  }

  try {
    const db = await mongoose.connect(
      URI ||
        "mongodb+srv://sagarmanchakatla02:zdVern62hVCbn7ct@cluster0.zehnh.mongodb.net/"
    );

    connection.isConnected = db.connections[0].readyState;

    console.log("MongoDB connected");
  } catch (error) {
    console.log("MongoDB connection error:", error);
    process.exit(1);
  }
}

export default dbConnect;
