import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { baseApiUrl } from '../../config'


export const graphApi = createApi({
    reducerPath: 'graphApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseApiUrl, credentials: "same-origin",}),
    endpoints: (builder) => ({
        getGraphCode: builder.query({
            query: (args) => {
                return { url : `v2/view_graph`, method: 'POST', body: {...args}}
            }
        }),
    }),
})

export const { useLazyGetGraphCodeQuery } = graphApi