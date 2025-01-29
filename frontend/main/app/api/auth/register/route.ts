import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import dbConnect from "@/lib/db";
import Manager from "@/models/Manger";
import Client from "@/models/Client";
import bcrypt from "bcryptjs";

export async function POST(req: NextRequest) {
  const { role, name, email, pass } = await req.json();
  console.log(role, name, email, pass);
  await dbConnect();

  if (!role || !["manager", "client"].includes(role)) {
    return NextResponse.json({ message: "Invalid role" }, { status: 400 });
  }

  const existingUser = await (role === "manager" ? Manager : Client).findOne({
    email,
  });
  if (existingUser)
    return NextResponse.json(
      { message: "Email already exists" },
      { status: 400 }
    );

  const hashedPass = await bcrypt.hash(pass, 10);

  const newUser =
    role === "manager"
      ? new Manager({ name, email, pass: hashedPass, clients: [] })
      : new Client({ name, email, pass: hashedPass, media_acc: {} });

  await newUser.save();
  return NextResponse.json(
    { message: `${role} registered successfully` },
    { status: 201 }
  );
}
