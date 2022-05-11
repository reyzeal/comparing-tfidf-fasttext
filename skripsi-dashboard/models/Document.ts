import mongoose, {Document} from "mongoose";
import paginate from "mongoose-paginate-v2";

export interface DocumentInterface extends Document{
    _id: string,
    data: object,
    type: string
}

const DocumentSchema = new mongoose.Schema<DocumentInterface>({
    _id: String,
    data: Object,
    type: String
})

DocumentSchema.plugin(paginate)

export default DocumentSchema;