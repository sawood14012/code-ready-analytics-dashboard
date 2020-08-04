"""Configuration of all relevant CI jobs."""
import configparser
from urllib.parse import urljoin


class CIJobs:
    """Class representing configuration of all relevant CI jobs."""

    CONFIG_FILE_NAME = 'ci_jobs.ini'

    JOB_TYPES = {"build_job", "test_job", "pylint_job", "pydoc_job", "smoketests"}

    def __init__(self):
        """Read and parse the configuration file."""
        self.config = configparser.ConfigParser()
        self.config.read(CIJobs.CONFIG_FILE_NAME)

    def get_ci_url(self):
        """Retrieve the URL to the CI front page."""
        return self.config.get('CI', 'jenkins_url')

    def get_badge_prefix(self):
        """Retrieve the prefix for any badge/icon."""
        return self.get_ci_url() + "/" + self.config.get('CI', 'badge_prefix')

    def get_job_url(self, repository_name, job_type):
        """Retrieve the URL to the CI job for given repository and job type."""
        assert job_type in CIJobs.JOB_TYPES
        # the job with given type might not exist, return None in such cases
        try:
            # remove prefix from repository name because we use shorter names in the INI file
            # repository_name = CIJobs.remove_prefix(repository_name, ["fabric8-analytics-",
            #                                                          "fabric8-"])
            url_prefix = self.get_ci_url()
            url_suffix = self.config.get(repository_name, job_type)
            return CIJobs.construct_job_url(url_prefix, url_suffix)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_job_name(self, repository_name, job_type):
        """Return the job name w/o the full URL to CI."""
        assert job_type in CIJobs.JOB_TYPES
        try:
            # remove prefix from repository name because we use shorter names in the INI file
            # repository_name = CIJobs.remove_prefix(repository_name, ["fabric8-analytics-",
            #                                                          "fabric8-"])
            url_suffix = self.config.get(repository_name, job_type)
            return url_suffix
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_job_badge(self, repository_name, job_type):
        """Return the URL to job badge."""
        assert job_type in CIJobs.JOB_TYPES
        try:
            url_prefix = self.get_badge_prefix()
            url_suffix = self.config.get(repository_name, job_type)
            url = url_prefix + "?job=" + url_suffix
            return url
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_console_output_url(self, repository_name):
        """Return URL that can be used to fetch console output of the last build."""
        try:
            job_url = self.get_job_url(repository_name, "test_job")
            if job_url is not None:
                return urljoin(job_url + "/", "lastSuccessfulBuild/consoleText")
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    @staticmethod
    def construct_job_url(url_prefix, url_suffix):
        """Construct the URL to job on CI from CI prefix and suffix with job name."""
        return urljoin(urljoin(url_prefix, "job/"), url_suffix)

    @staticmethod
    def remove_prefix(text, prefixes):
        """Remove the prefix from input string (if the string starts with prefix)."""
        for prefix in prefixes:
            if text.startswith(prefix):
                return text[len(prefix):]
        return text
