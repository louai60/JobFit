import React, { useEffect, useState } from 'react';
import { getResumeDetails } from '../services/resumeService';
import { useParams } from 'react-router-dom';
import { toast } from 'sonner';

export const ResumeDetails = () => {
  const { resumeId } = useParams<{ resumeId: string }>();
  const [resume, setResume] = useState<any>(null);

  useEffect(() => {
    const id = Number(resumeId);
    if (isNaN(id)) {
      toast.error('Invalid resume ID');
      return;
    }

    const fetchDetails = async () => {
      try {
        const data = await getResumeDetails(id);
        setResume(data);
      } catch (error: any) {
        toast.error(error.message);
      }
    };

    fetchDetails();
  }, [resumeId]);

  const skillsList = resume && Array.isArray(resume.skills) ? resume.skills.join(', ') : 'No skills listed';

  return (
    <div>
      {resume ? (
        <div>
          <h1>Resume Details</h1>
          <p>Skills: {skillsList}</p>
          <p>Experience: {resume.experience}</p>
          <p>Education: {resume.education}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}; 