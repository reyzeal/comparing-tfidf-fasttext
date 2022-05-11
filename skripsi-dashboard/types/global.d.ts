import mongoose from "mongoose";
import {ModelsInterface} from "../models";

export {};

declare global{
    var db = {
        conn: mongoose.Connection,
        promise: Promise<mongoose.Connection>(),
        models: ModelsInterface
    };
}