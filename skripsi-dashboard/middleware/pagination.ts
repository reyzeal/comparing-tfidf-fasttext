import {NextApiRequest} from "next"

const handler = (req: NextApiRequest) => {
    return {
        limit: parseInt(req.query.limit as string) || 10,
        page: parseInt(req.query.page as string) || 1,
    }
}

export default handler