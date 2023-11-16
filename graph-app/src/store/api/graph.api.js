import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { baseApiUrl } from '../../config'


export const graphApi = createApi({
    reducerPath: 'graphApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseApiUrl, credentials: "same-origin",}),
    endpoints: (builder) => ({
        getGraphCode: builder.query({
            query: (args) => {
                const { codeText, language, graphType } = args
                return { url : `view_graph?code=${codeText}&lang=${language}&model=${graphType}`}
            }
        }),
    }),
})

export const { useLazyGetGraphCodeQuery } = graphApi