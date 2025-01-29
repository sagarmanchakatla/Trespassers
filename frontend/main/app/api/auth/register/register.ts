import type { NextApiRequest, NextApiResponse } from "next";
import dbConnect from "@/lib/db";
import Manager from "@/models/Manger";
import Client from "@/models/Client";
import bcrypt from "bcryptjs";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "POST")
    return res.status(405).json({ message: "Method Not Allowed" });

  await dbConnect();
  const { role, name, email, pass } = req.body;

  if (!role || !["manager", "client"].includes(role)) {
    return res.status(400).json({ message: "Invalid role" });
  }

  const existingUser = await (role === "manager" ? Manager : Client).findOne({
    email,
  });
  if (existingUser)
    return res.status(400).json({ message: "Email already exists" });

  const hashedPass = await bcrypt.hash(pass, 10);

  const newUser =
    role === "manager"
      ? new Manager({ name, email, pass: hashedPass, clients: [] })
      : new Client({ name, email, pass: hashedPass, media_acc: {} });

  await newUser.save();
  res.status(201).json({ message: `${role} registered successfully` });
}
