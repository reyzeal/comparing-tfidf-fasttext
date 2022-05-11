// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import dbConnect from "../../../lib/dbConnect";
import fetch from 'isomorphic-unfetch'

type Data = {
    ok: boolean,
    message: string
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
) {
    const {Document} = await dbConnect()

    return fetch("http://eprints.upnyk.ac.id/cgi/search/archive/advanced/export_eprints_JSON.js?dataset=archive&screen=Search&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive%7C-%7Cdepartment%3Adepartment%3AALL%3AIN%3AINFORMATIKA%7Ctype%3Atype%3AANY%3AEQ%3Athesis%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n=&cache=152949")
        .then(r => r.json())
        .then(async r => {
            await Document.deleteMany({
                type: "raw"
            }).exec()

            const bulk = Document.collection.initializeOrderedBulkOp()
            for(let i of r){
                bulk.insert({
                    _id: i.eprintid,
                    data: i,
                    type: "raw"
                })
            }
            await bulk.execute(console.log)
            res.json({
                ok: true,
                message: "Sukses"
            })
        })
}
