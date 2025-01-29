import mongoose, { Schema, Document } from "mongoose";

export interface IClient extends Document {
  name: string;
  email: string;
  pass: string;
  media_acc: {
    yt?: string;
    insta?: string;
    x?: string;
  };
}

const ClientSchema = new Schema<IClient>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  pass: { type: String, required: true },
  media_acc: {
    yt: { type: String, default: "" },
    insta: { type: String, default: "" },
    x: { type: String, default: "" },
  },
});

export default mongoose.models.Client ||
  mongoose.model<IClient>("Client", ClientSchema);
