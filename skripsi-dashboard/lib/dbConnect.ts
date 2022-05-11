import mongoose from "mongoose"
import Models, {ModelsInterface} from "../models";

async function dbConnect():Promise<ModelsInterface> {
    let connections = mongoose.connections
    if(connections.length && connections[0].readyState !== 1){
        await mongoose.connect(process.env.MONGODB_URL||"mongodb://localhost:27017/skripsi")
        if(!Object.keys(mongoose.models).length) {
            Models()
        }
    }

    return mongoose.models as unknown as ModelsInterface
}

export default dbConnect