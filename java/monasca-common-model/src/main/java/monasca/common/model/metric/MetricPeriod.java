/*
 * Copyright 2016 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package monasca.common.model.metric;

/**
 * Utility class to determine periodicity or infrequency
 * of given metric.
 */
public class MetricPeriod {
  /**
   * Defines threshold that if compared with
   * period value answers is metric is periodic or sporadic
   */
  private static final long THRESHOLD = 0L;

  private MetricPeriod() {
  }

  public static boolean isSporadic(final Metric metric) {
    return metric != null && isSporadic(metric.getPeriod());
  }

  public static boolean isSporadic(final long period) {
    return period < THRESHOLD;
  }

  public static boolean isPeriodic(final Metric metric) {
    return metric != null && isPeriodic(metric.getPeriod());
  }

  public static boolean isPeriodic(final long period) {
    return period > THRESHOLD;
  }

}
