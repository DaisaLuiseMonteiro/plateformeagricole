/**
 * Utility to upload images to Cloudinary using an Unsigned Upload Preset.
 */

const CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/dps0wgmoa/image/upload';
const UPLOAD_PRESET = 'agroconnect_preset';

/**
 * Uploads a file to Cloudinary.
 * @param file The image file to upload (from an <input type="file"> or Drag & Drop)
 * @returns Promise<string> The secure URL of the uploaded image
 */
export const uploadToCloudinary = async (file: File): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('upload_preset', UPLOAD_PRESET);

  try {
    const response = await fetch(CLOUDINARY_URL, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'Failed to upload image to Cloudinary');
    }

    const data = await response.json();
    return data.secure_url;
  } catch (error) {
    console.error('Error uploading to Cloudinary:', error);
    throw error;
  }
};
