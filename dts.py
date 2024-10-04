from multiprocessing import AuthenticationError
import httpx
from bs4 import BeautifulSoup


class DTS:
    """
    A class to interact with the PUP DTS (Document Tracking System).

    Attributes:
        email (str): The email address used for authentication.
        password (str): The password used for authentication.
        session (httpx.Client): The HTTP client session used for making requests.
        csrfofes (str): The CSRF token obtained after login.
        sessid (str): The session ID obtained after login.

    Methods:
        login():
            Authenticates the user with the provided email and password.
        track(dts_num):
            Tracks a document using the provided DTS number.
        fetch_document_details(trace_page):
            Fetches the details of a document from the provided trace page URL.
    """

    def __init__(self, email, password):
        """
        Initializes the DTS object with user credentials and sets up the session for requests.

        Args:
            email (str): The email address used for authentication.
            password (str): The password used for authentication.

        Raises:
            AuthenticationError: If login fails after multiple retries.
        """
        self.email = email
        self.password = password
        self.session = httpx.Client()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
        )

        self.csrfofes = None
        self.sessid = None
        self.login()

    def login(self):
        """
        Authenticates the user using the provided email and password, retrieves the CSRF token and session ID.

        Raises:
            AuthenticationError: If login fails after multiple retries or if the credentials are invalid.
        """
        login_url = "https://apps.pup.edu.ph/dts/site/authentication"
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                response = self.session.get(login_url)
                if response.status_code == 200:
                    self.csrfofes = response.cookies.get("csrfofes_ck")
                    self.sessid = response.cookies.get("PHPSESSID")
                    break
            except httpx.RequestError:
                retries += 1
                if retries == max_retries:
                    raise AuthenticationError(
                        "Maximum retries reached while accessing the login page, please try again later."
                    )

        login_payload = {
            "email": self.email,
            "password": self.password,
            "csrfofes_tk": self.csrfofes,
            "btnSignIn": "Sign In",
        }

        response = self.session.post(login_url, data=login_payload)
        if response.status_code != 200:
            raise AuthenticationError(
                "Failed to log in. Please check your credentials."
            )

    def track(self, dts_num):
        """
        Tracks a document using the provided DTS number.

        Args:
            dts_num (str): The DTS number of the document to track.

        Returns:
            dict: A dictionary containing document details and action items.

        Raises:
            Exception: If there is an error while searching for the DTS number.
        """
        trace_url = "https://apps.pup.edu.ph/dts/document/trace/"
        trace_payload = {
            "csrfofes_tk": self.csrfofes,
            "keyword": dts_num,
            "btnTrace": "Trace",
            "table1_length": "10",
        }

        response = self.session.post(trace_url, data=trace_payload)
        if response.status_code != 200:
            raise Exception(
                "An error occurred while searching the DTS Number. Please try again later."
            )

        soup = BeautifulSoup(response.text, "lxml")
        first_link = soup.find("table", id="table1").find("a")
        dts_link = first_link["href"] if first_link else None

        if not dts_link:
            return {"error": "No link found for the provided DTS number."}

        trace_page = "https://apps.pup.edu.ph" + dts_link
        return self.fetch_document_details(trace_page)

    def fetch_document_details(self, trace_page):
        """
        Fetches detailed information about a document from the provided trace page URL.

        Args:
            trace_page (str): The URL of the document trace page.

        Returns:
            dict: A dictionary containing document details and action items.

        Raises:
            Exception: If there is an error while accessing the document page.
        """
        response = self.session.get(trace_page)
        if response.status_code != 200:
            raise Exception(
                "An error occurred while accessing the document page. Please try again later."
            )

        soup = BeautifulSoup(response.text, "lxml")
        details = {}

        # Extract document details
        for dt in soup.find_all("dt"):
            detail_name = dt.get_text(strip=True)
            if detail_name in [
                "Title",
                "Details",
                "Signatory",
                "Status",
                "Current Department",
                "Assigned To",
                "Last Update",
                "Date Created",
                "Document Type",
                "Origin Department",
            ]:
                dd = dt.find_next("dd")
                details[detail_name] = dd.get_text(strip=True)

        section_content = soup.find("section", class_="content")
        items = []

        # Extract action items
        if section_content:
            for item in section_content.find_all("li", class_="item"):
                office_staff_element = item.find("a", class_="product-title")
                if office_staff_element:
                    office_full = office_staff_element.text.strip()
                    staff_badge = office_staff_element.find("span", class_="badge")
                    staff = staff_badge.text if staff_badge else "No badge"
                    office = office_full.replace(staff, "").strip()

                    # Combine office and staff with a hyphen
                    office_staff_combined = f"{office} - {staff}"

                    action = {
                        "date_time": item.find("div", class_="product-info")
                        .text.strip()
                        .split("\n")[0]
                        .rstrip(),
                        "office_staff": office_staff_combined,
                        "status": item.find("b", class_="text-muted").text
                        if item.find("b", class_="text-muted")
                        else "No status",
                        "detail_text": item.find("div", class_="text-justify").get_text(
                            strip=True
                        )
                        if item.find("div", class_="text-justify")
                        else "No additional details",
                    }
                    items.append(action)

        return {"details": details, "action_items": items}
