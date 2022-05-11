import mongoose from "mongoose";
import document, {DocumentInterface} from "./Document";
export interface ModelsInterface {
    Document : mongoose.PaginateModel<DocumentInterface>,
}
export default () => {
    return {
        Document : mongoose.model<DocumentInterface, mongoose.PaginateModel<DocumentInterface>>("Document", document)
    }
}