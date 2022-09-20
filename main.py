import requests
from bs4 import BeautifulSoup
import hashlib
from os.path import exists
from datetime import datetime
import time
import os
from send_email import sendRyobiAvailabilityNotificationEmail
import sys

# Useful if website is blocking based on user agent -
# Example: Home Depot will not return responses for the default 'requests' user agent
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
                         "Safari/537.36"}

URL = ""
BASIC_AUTH_USERNAME = None
BASIC_AUTH_PASSWORD = None
# Update this to anything you want to use as the 'seed' for the change hash
# Ideally it is a region or set of values that a page has that you want to watch.
SOUP_FIND_ALL_CONDITION = "table"
FILENAME = "ProductAvailabilityLog.txt"

headers = {
    'origin': 'https://www.homedepot.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'x-current-url': '/p/RYOBI-ONE-18V-Cordless-SWIFTClean-Spot-Cleaner-Tool-Only-PCL756B/319962906',
    'x-experience-name': 'general-merchandise',
}

params = {
    'opname': 'productClientOnlyProduct',
}

json_body_data = {
    'operationName': 'productClientOnlyProduct',
    'variables': {
        'skipSpecificationGroup': False,
        'skipSubscribeAndSave': False,
        'skipKPF': False,
        'skipInstallServices': True,
        'itemId': '319962906',
        'storeId': '475',
        'zipCode': '85383',
    },
    'query': 'query productClientOnlyProduct($storeId: String, $zipCode: String, $quantity: Int, $itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $skipKPF: Boolean = false, $skipInstallServices: Boolean = true) {\n  product(itemId: $itemId, dataSource: $dataSource, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    fulfillment(storeId: $storeId, zipCode: $zipCode, quantity: $quantity) {\n      backordered\n      fulfillmentOptions {\n        type\n        services {\n          type\n          locations {\n            isAnchor\n            locationId\n            inventory {\n              isOutOfStock\n              quantity\n              isInStock\n              isLimitedQuantity\n              isUnavailable\n              maxAllowedBopisQty\n              minAllowedBopisQty\n              __typename\n            }\n            curbsidePickupFlag\n            isBuyInStoreCheckNearBy\n            distance\n            storeName\n            state\n            type\n            storePhone\n            __typename\n          }\n          hasFreeShipping\n          freeDeliveryThreshold\n          optimalFulfillment\n          deliveryTimeline\n          deliveryDates {\n            startDate\n            endDate\n            __typename\n          }\n          deliveryCharge\n          dynamicEta {\n            hours\n            minutes\n            __typename\n          }\n          totalCharge\n          __typename\n        }\n        fulfillable\n        __typename\n      }\n      backorderedShipDate\n      bossExcludedShipStates\n      excludedShipStates\n      seasonStatusEligible\n      anchorStoreStatus\n      anchorStoreStatusType\n      sthExcludedShipState\n      bossExcludedShipState\n      onlineStoreStatus\n      onlineStoreStatusType\n      inStoreAssemblyEligible\n      __typename\n    }\n    info {\n      dotComColorEligible\n      hidePrice\n      ecoRebate\n      quantityLimit\n      sskMin\n      sskMax\n      unitOfMeasureCoverage\n      wasMaxPriceRange\n      wasMinPriceRange\n      fiscalYear\n      productDepartment\n      classNumber\n      forProfessionalUseOnly\n      globalCustomConfigurator {\n        customButtonText\n        customDescription\n        customExperience\n        customExperienceUrl\n        customTitle\n        __typename\n      }\n      paintBrand\n      movingCalculatorEligible\n      label\n      prop65Warning\n      returnable\n      hasSubscription\n      isBuryProduct\n      isSponsored\n      isGenericProduct\n      isLiveGoodsProduct\n      sponsoredBeacon {\n        onClickBeacon\n        onViewBeacon\n        __typename\n      }\n      sponsoredMetadata {\n        campaignId\n        placementId\n        slotId\n        __typename\n      }\n      productSubType {\n        name\n        link\n        __typename\n      }\n      categoryHierarchy\n      samplesAvailable\n      customerSignal {\n        previouslyPurchased\n        __typename\n      }\n      productDepartmentId\n      augmentedReality\n      swatches {\n        isSelected\n        itemId\n        label\n        swatchImgUrl\n        url\n        value\n        __typename\n      }\n      totalNumberOfOptions\n      recommendationFlags {\n        visualNavigation\n        batItems\n        packages\n        __typename\n      }\n      pipCalculator {\n        toggle\n        coverageUnits\n        display\n        publisher\n        __typename\n      }\n      replacementOMSID\n      minimumOrderQuantity\n      projectCalculatorEligible\n      subClassNumber\n      calculatorType\n      protectionPlanSku\n      hasServiceAddOns\n      consultationType\n      __typename\n    }\n    itemId\n    dataSources\n    identifiers {\n      canonicalUrl\n      brandName\n      itemId\n      modelNumber\n      productLabel\n      storeSkuNumber\n      upcGtin13\n      specialOrderSku\n      toolRentalSkuNumber\n      rentalCategory\n      rentalSubCategory\n      upc\n      productType\n      isSuperSku\n      parentId\n      roomVOEnabled\n      sampleId\n      __typename\n    }\n    availabilityType {\n      discontinued\n      status\n      type\n      buyable\n      __typename\n    }\n    details {\n      description\n      collection {\n        url\n        collectionId\n        name\n        __typename\n      }\n      highlights\n      descriptiveAttributes {\n        name\n        value\n        bulleted\n        sequence\n        __typename\n      }\n      additionalResources {\n        infoAndGuides {\n          name\n          url\n          __typename\n        }\n        installationAndRentals {\n          contentType\n          name\n          url\n          __typename\n        }\n        diyProjects {\n          contentType\n          name\n          url\n          __typename\n        }\n        __typename\n      }\n      installation {\n        leadGenUrl\n        __typename\n      }\n      __typename\n    }\n    media {\n      images {\n        url\n        type\n        subType\n        sizes\n        __typename\n      }\n      video {\n        shortDescription\n        thumbnail\n        url\n        videoStill\n        link {\n          text\n          url\n          __typename\n        }\n        title\n        type\n        videoId\n        longDescription\n        __typename\n      }\n      threeSixty {\n        id\n        url\n        __typename\n      }\n      augmentedRealityLink {\n        usdz\n        image\n        __typename\n      }\n      richContent {\n        content\n        displayMode\n        richContentSource\n        salsifyRichContent\n        __typename\n      }\n      __typename\n    }\n    pricing(storeId: $storeId) {\n      promotion {\n        dates {\n          end\n          start\n          __typename\n        }\n        type\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        dollarOff\n        percentageOff\n        savingsCenter\n        savingsCenterPromos\n        specialBuySavings\n        specialBuyDollarOff\n        specialBuyPercentageOff\n        experienceTag\n        subExperienceTag\n        itemList\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      value\n      alternatePriceDisplay\n      alternate {\n        bulk {\n          pricePerUnit\n          thresholdQuantity\n          value\n          __typename\n        }\n        unit {\n          caseUnitOfMeasure\n          unitsOriginalPrice\n          unitsPerCase\n          value\n          __typename\n        }\n        __typename\n      }\n      original\n      mapAboveOriginalPrice\n      message\n      preferredPriceFlag\n      specialBuy\n      unitOfMeasure\n      conditionalPromotions {\n        dates {\n          start\n          end\n          __typename\n        }\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        experienceTag\n        subExperienceTag\n        eligibilityCriteria {\n          itemGroup\n          minPurchaseAmount\n          minPurchaseQuantity\n          relatedSkusCount\n          omsSkus\n          __typename\n        }\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      ratingsReviews {\n        averageRating\n        totalReviews\n        __typename\n      }\n      __typename\n    }\n    seo {\n      seoKeywords\n      seoDescription\n      __typename\n    }\n    specificationGroup @skip(if: $skipSpecificationGroup) {\n      specifications {\n        specName\n        specValue\n        __typename\n      }\n      specTitle\n      __typename\n    }\n    taxonomy {\n      breadCrumbs {\n        label\n        url\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionName\n        refinementKey\n        __typename\n      }\n      brandLinkUrl\n      __typename\n    }\n    favoriteDetail {\n      count\n      __typename\n    }\n    sizeAndFitDetail {\n      attributeGroups {\n        attributes {\n          attributeName\n          dimensions\n          __typename\n        }\n        dimensionLabel\n        productType\n        __typename\n      }\n      __typename\n    }\n    subscription @skip(if: $skipSubscribeAndSave) {\n      defaultfrequency\n      discountPercentage\n      subscriptionEnabled\n      __typename\n    }\n    badges(storeId: $storeId) {\n      label\n      name\n      color\n      creativeImageUrl\n      endDate\n      message\n      timerDuration\n      timer {\n        timeBombThreshold\n        daysLeftThreshold\n        dateDisplayThreshold\n        message\n        __typename\n      }\n      __typename\n    }\n    keyProductFeatures @skip(if: $skipKPF) {\n      keyProductFeaturesItems {\n        features {\n          name\n          refinementId\n          refinementUrl\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    dataSource\n    installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n      scheduleAMeasure\n      gccCarpetDesignAndOrderEligible\n      __typename\n    }\n    seoDescription\n    __typename\n  }\n}\n',
}

SMTP_USERNAME = None  # Gets set on startup from OS environment variables
SMTP_PASSWORD = None  # Gets set on startup from OS environment variables
EMAIL_ADDRESS = ""  # Gets set from program arguments (single email address string)

def jsonDataWatcher():
    response = requests.post('https://www.homedepot.com/federation-gateway/graphql',
                             params=params,
                             headers=headers,
                             json=json_body_data)
    return response.json()["data"]["product"]["fulfillment"]["fulfillmentOptions"]


def dataHasChanged(hash):
    file = open(FILENAME, 'r')
    lastLine = file.readlines()[-1].split('~')[1]
    return lastLine.strip() != str(hash)


def generateSiteHash():
    if BASIC_AUTH_USERNAME is not None:
        page = requests.get(URL, auth=(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))
    else:
        page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser").findAll(SOUP_FIND_ALL_CONDITION)
    return hashlib.md5(str(soup).encode('utf-8')).hexdigest()


def saveHashToFile(hash):
    file = open(FILENAME, "a")
    dateTimeNow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    file.write(dateTimeNow + '~' + str(hash) + '\n')
    file.close()


def setup():
    if not exists(FILENAME):
        print("First time run detected")
        open(FILENAME, 'w').close()
        saveHashToFile(jsonDataWatcher())
        print("File setup complete, let the watching begin")
        # exit()


def run():
    notificationEmailSent = False

    while True:
        pageHash = jsonDataWatcher()
        if dataHasChanged(pageHash):
            print("Detected that the product availability has changed!")
            saveHashToFile(pageHash)
            for i in range(0, 60):
                if not notificationEmailSent:
                    print("Sending notification email!")
                    sendRyobiAvailabilityNotificationEmail(SMTP_USERNAME, SMTP_PASSWORD, EMAIL_ADDRESS)
                    notificationEmailSent = True
                # This will make a notification sound on macOS, only if this script is run from a terminal
                print("Hey, look at me! It appears the product might be available!")
                print('\a\a\a')

                time.sleep(60)
            print("Alright... I am tired. I quit.")
            exit(0)
        else:
            print("Website is the same as it was before")
        print("Waiting 1 hour until next check")
        time.sleep(3600)


if __name__ == "__main__":
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    if SMTP_USERNAME is None or SMTP_PASSWORD is None:
        print("ERROR: ERROR: Missing SMTP_USERNAME or SMTP_PASSWORD environment variables.\nPlease set these and "
              "restart this script.")
        exit(1)

    if len(sys.argv) > 1:
        EMAIL_ADDRESS = sys.argv[1]
    else:
        print('No parameter supplied for email address. Please pass 1 email address as a parameter')
        print('Usage:\n1st = Email address to send notification to')
        exit(2)
    setup()
    run()
