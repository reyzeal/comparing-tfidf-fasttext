import {NextApiRequest, NextApiResponse} from "next";
import dbConnect from "../../../lib/dbConnect";
import {Api} from "../../../interfaces/api";
import pagination from "../../../middleware/pagination";

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Api>
) {
    let paginationOpt = pagination(req)
    const {Document} = await dbConnect()

    const page = await Document.paginate({
        type: "raw"
    }, paginationOpt)

    return res.json({
        ok: true,
        message: "berhasil",
        data: page
    })
}