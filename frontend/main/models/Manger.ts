import mongoose, { Schema, Document, Types } from "mongoose";

export interface IManager extends Document {
  name: string;
  email: string;
  pass: string;
  clients: Types.ObjectId[];
}

const ManagerSchema = new Schema<IManager>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  pass: { type: String, required: true },
  clients: [{ type: Schema.Types.ObjectId, ref: "Client" }],
});

export default mongoose.models.Manager ||
  mongoose.model<IManager>("Manager", ManagerSchema);
