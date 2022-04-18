import useAxios from '../useAxios'

const uploads_endpoint = "upload"

export const useUploads = () => {
    const { get, post} = useAxios();

    return {
        upload: (params: any) =>
            post(`${uploads_endpoint}/`, params),
    }

}
