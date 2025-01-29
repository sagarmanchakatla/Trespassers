import type { NextApiRequest, NextApiResponse } from "next";
import dbConnect from "@/lib/db";
import Manager from "@/models/Manger";
import Client from "@/models/Client";
import { verify } from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET || "your_jwt_secret";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== "GET")
    return res.status(405).json({ message: "Method Not Allowed" });

  await dbConnect();

  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ message: "Unauthorized" });

  try {
    const decoded = verify(token, JWT_SECRET) as { id: string };
    const user =
      (await Manager.findById(decoded.id)) ||
      (await Client.findById(decoded.id));
    if (!user) return res.status(404).json({ message: "User not found" });

    res.status(200).json({ user });
  } catch (error) {
    res.status(401).json({ message: "Invalid token" });
  }
}
