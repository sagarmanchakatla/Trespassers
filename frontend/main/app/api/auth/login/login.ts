import type { NextApiRequest, NextApiResponse } from "next";
import dbConnect from "@/lib/db";
import Manager from "@/models/Manager";
import Client from "@/models/Client";
import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";

const JWT_SECRET = process.env.JWT_SECRET || "your_jwt_secret";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST")
    return res.status(405).json({ message: "Method Not Allowed" });

  await dbConnect();
  const { email, pass } = req.body;

  const user =
    (await Manager.findOne({ email })) || (await Client.findOne({ email }));
  if (!user) return res.status(400).json({ message: "Invalid credentials" });

  const isMatch = await bcrypt.compare(pass, user.pass);
  if (!isMatch) return res.status(400).json({ message: "Invalid credentials" });

  const token = jwt.sign({ id: user._id, email: user.email }, JWT_SECRET, {
    expiresIn: "1h",
  });

  res.status(200).json({
    token,
    userId: user._id,
    role: user instanceof Manager ? "manager" : "client",
  });
}
